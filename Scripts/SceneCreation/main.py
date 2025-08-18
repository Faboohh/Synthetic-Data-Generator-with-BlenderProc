import blenderproc as bproc
import argparse
import numpy as np
import os
import random

parser = argparse.ArgumentParser()
parser.add_argument("--camera", required=True)
parser.add_argument("--obj", required=True)
parser.add_argument("--second_obj")  # Optional
parser.add_argument("--texture_dir", required=True)     
parser.add_argument("--output_dir", required=True)
args = parser.parse_args()

bproc.init()

main_obj = bproc.loader.load_obj(args.obj)[0]

# Optional second object
second_obj = None
if args.second_obj:
    second_obj = bproc.loader.load_obj(args.second_obj)[0]

# Align main object to the floor
bbox = np.array(main_obj.get_bound_box())
min_z = np.min(bbox[:, 2])
main_obj.set_location(main_obj.get_location() - np.array([0, 0, min_z]))

main_obj.enable_rigidbody(False)
main_obj.set_cp("category_id", 1)

# Add dust
for material in main_obj.get_materials():
    bproc.material.add_dust(material, strength=2, texture_scale=0.05)

# Create floor
floor = bproc.object.create_primitive("PLANE", scale=[5, 5, 1])
floor.set_location([0, 0, 0])

cc_materials = bproc.loader.load_ccmaterials(args.texture_dir)
if not cc_materials:
    raise RuntimeError(f"No CCTextures found in directory: {args.texture_dir}")

floor_mat = random.choice(cc_materials)
floor.replace_materials(floor_mat)

# Apply random material to main object
obj_mat = random.choice(cc_materials)
main_obj.replace_materials(obj_mat)

# If second object is present, load and position it
if second_obj:
    # Align table (second object) to the house floor
    second_bbox = np.array(second_obj.get_bound_box())
    table_current_z = np.min(second_bbox[:, 2])
    main_bbox = np.array(main_obj.get_bound_box())
    house_floor_z = np.min(main_bbox[:, 2]) + 0.01
    z_offset = house_floor_z - table_current_z

    # Set location (adjust as needed)
    second_obj.set_location(second_obj.get_location() + np.array([0, 0, z_offset]))
    second_obj.set_location(second_obj.get_location() + np.array([0, 0, 0.265]))

    second_obj.enable_rigidbody(False)
    second_obj.set_cp("category_id", 2)

    # Apply material
    second_obj_mat = random.choice(cc_materials)
    second_obj.replace_materials(second_obj_mat)

# Load camera poses
with open(args.camera, "r") as f:
    for line in f.readlines():
        vals = [float(x) for x in line.strip().split()]
        position, euler_rotation = vals[:3], vals[3:6]
        matrix_world = bproc.math.build_transformation_mat(position, euler_rotation)
        bproc.camera.add_camera_pose(matrix_world)
        bproc.camera.set_resolution(1920, 1080)

# Lights
light = bproc.types.Light()
light.set_type("POINT")
light.set_location([0.057095, -0.204272, 0.539142])
light.set_energy(500)

light2 = bproc.types.Light()
light2.set_type("POINT")
light2.set_location([3, 3, 4])
light2.set_energy(2000)

# Rendering setup
bproc.renderer.set_output_format(enable_transparency=False)
bproc.renderer.enable_normals_output()
bproc.renderer.enable_depth_output(activate_antialiasing=True)
instance_segmaps = bproc.renderer.enable_segmentation_output(map_by=["instance"])

data = bproc.renderer.render()

# Write to HDF5
bproc.writer.write_hdf5(args.output_dir, data)
