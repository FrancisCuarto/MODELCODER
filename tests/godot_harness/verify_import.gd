extends SceneTree

func _init():
	var args = OS.get_cmdline_user_args()
	if args.is_empty():
		_fail("No GLB filepath provided in user arguments (-- <path>)")
		return

	var glb_path = args[0]
	if not FileAccess.file_exists(glb_path):
		_fail("File does not exist on disk: " + glb_path)
		return

	var root_node: Node = null
	if ResourceLoader.exists(glb_path):
		var res = ResourceLoader.load(glb_path)
		if res is PackedScene:
			root_node = res.instantiate()

	if not root_node:
		var gltf_doc = GLTFDocument.new()
		var gltf_state = GLTFState.new()
		var err = gltf_doc.append_from_file(glb_path, gltf_state)
		if err != OK:
			_fail("GLTFDocument.append_from_file failed with error code: " + str(err))
			return
		root_node = gltf_doc.generate_scene(gltf_state)

	if not root_node:
		_fail("Could not load scene as PackedScene or generate via GLTFDocument")
		return

	var report = {
		"valid": true,
		"file": glb_path,
		"root_name": root_node.name,
		"root_class": root_node.get_class(),
		"mesh_count": 0,
		"static_body_count": 0,
		"collision_shape_count": 0,
		"socket_count": 0,
		"total_surfaces": 0,
		"materials": [],
		"sockets": [],
		"nodes": [],
		"bounds_aabb": {
			"position": [0.0, 0.0, 0.0],
			"size": [0.0, 0.0, 0.0]
		},
		"warnings": [],
		"errors": []
	}

	var global_aabb = AABB()
	var first_mesh = true

	_traverse_node(root_node, 0, report, global_aabb, first_mesh)

	if not first_mesh:
		report["bounds_aabb"]["position"] = [
			snapped(global_aabb.position.x, 0.001),
			snapped(global_aabb.position.y, 0.001),
			snapped(global_aabb.position.z, 0.001)
		]
		report["bounds_aabb"]["size"] = [
			snapped(global_aabb.size.x, 0.001),
			snapped(global_aabb.size.y, 0.001),
			snapped(global_aabb.size.z, 0.001)
		]

	if report["mesh_count"] == 0:
		report["warnings"].append("Scene contains no MeshInstance3D nodes")

	print("---GODOT_VALIDATION_JSON_START---")
	print(JSON.stringify(report, "\t"))
	print("---GODOT_VALIDATION_JSON_END---")

	root_node.free()
	quit(0)

func _fail(reason: String):
	var err_report = {
		"valid": false,
		"errors": [reason]
	}
	print("---GODOT_VALIDATION_JSON_START---")
	print(JSON.stringify(err_report, "\t"))
	print("---GODOT_VALIDATION_JSON_END---")
	quit(1)

func _traverse_node(node: Node, depth: int, report: Dictionary, global_aabb: AABB, first_mesh: bool):
	var node_data = {
		"name": node.name,
		"class": node.get_class(),
		"depth": depth
	}

	# Check for socket empties / attach points
	var lower_name = node.name.to_lower()
	if lower_name.begins_with("socket_") or lower_name.contains("-attach"):
		report["socket_count"] += 1
		report["sockets"].append({
			"name": node.name,
			"position": [
				snapped(node.position.x, 0.001),
				snapped(node.position.y, 0.001),
				snapped(node.position.z, 0.001)
			] if node is Node3D else [0, 0, 0]
		})

	if node is StaticBody3D:
		report["static_body_count"] += 1
	elif node is CollisionShape3D:
		report["collision_shape_count"] += 1
		if node.shape:
			node_data["shape_class"] = node.shape.get_class()
	elif node is MeshInstance3D:
		report["mesh_count"] += 1
		var mesh = node.mesh
		if mesh:
			var sc = mesh.get_surface_count()
			node_data["surface_count"] = sc
			report["total_surfaces"] += sc

			var aabb = node.get_aabb()
			node_data["aabb"] = {
				"position": [snapped(aabb.position.x, 0.001), snapped(aabb.position.y, 0.001), snapped(aabb.position.z, 0.001)],
				"size": [snapped(aabb.size.x, 0.001), snapped(aabb.size.y, 0.001), snapped(aabb.size.z, 0.001)]
			}

			# Check for Godot collision suffix convention
			if lower_name.ends_with("-convcolonly") or lower_name.ends_with("-convcol"):
				var conv_shape = mesh.create_convex_shape(true, false)
				if conv_shape:
					report["static_body_count"] += 1
					report["collision_shape_count"] += 1
					node_data["godot_collision"] = {
						"shape": "ConvexPolygonShape3D",
						"points": conv_shape.points.size(),
						"strips_visual_mesh": lower_name.ends_with("-convcolonly")
					}
			elif lower_name.ends_with("-colonly") or lower_name.ends_with("-col"):
				var tri_shape = mesh.create_trimesh_shape()
				if tri_shape:
					report["static_body_count"] += 1
					report["collision_shape_count"] += 1
					node_data["godot_collision"] = {
						"shape": "ConcavePolygonShape3D",
						"faces": tri_shape.faces.size() / 3,
						"strips_visual_mesh": lower_name.ends_with("-colonly")
					}

			# Only merge visual meshes into visual bounds if not collision-only
			var is_col_only = lower_name.ends_with("-convcolonly") or lower_name.ends_with("-colonly")
			if not is_col_only:
				if first_mesh:
					global_aabb = aabb
					first_mesh = false
				else:
					global_aabb = global_aabb.merge(aabb)

			var mats = []
			var has_uv = false
			for s in range(sc):
				var arrays = mesh.surface_get_arrays(s)
				if arrays.size() > Mesh.ARRAY_TEX_UV and arrays[Mesh.ARRAY_TEX_UV] != null:
					if arrays[Mesh.ARRAY_TEX_UV].size() > 0:
						has_uv = true
				var mat = node.get_surface_override_material(s)
				if not mat:
					mat = mesh.surface_get_material(s)
				var mat_name = mat.resource_name if mat else "None"
				mats.append(mat_name)
				if not mat_name in report["materials"]:
					report["materials"].append(mat_name)
			node_data["materials"] = mats
			node_data["has_uv"] = has_uv
			if not is_col_only and not has_uv:
				report["warnings"].append("Visual mesh '" + node.name + "' has no UV coordinates (ARRAY_TEX_UV missing)")

	report["nodes"].append(node_data)

	for child in node.get_children():
		_traverse_node(child, depth + 1, report, global_aabb, first_mesh)
