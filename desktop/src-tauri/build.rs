fn main() {
    tauri_build::try_build(
        tauri_build::Attributes::new()
            .app_manifest(
                tauri_build::AppManifest::new()
                    .commands(&[
                        "get_textures_dir",
                        "list_local_textures",
                        "read_local_texture_data_url",
                        "import_texture_to_folder",
                        "open_textures_folder",
                        "export_to_disk",
                        "open_external_url",
                        "save_project_dialog"
                    ])
            ),
    ).unwrap();
}
