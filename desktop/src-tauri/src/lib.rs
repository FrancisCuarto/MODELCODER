use std::fs;
use std::path::PathBuf;
use base64::Engine;

/// Returns the local path where custom user textures are stored:
/// e.g. `%USERPROFILE%/Documents/ModelCoder/Textures` on Windows
#[tauri::command]
fn get_textures_dir() -> Result<String, String> {
    let base = std::env::var("USERPROFILE")
        .or_else(|_| std::env::var("HOME"))
        .unwrap_or_else(|_| ".".to_string());
    let path = PathBuf::from(base).join("Documents").join("ModelCoder").join("Textures");
    let _ = fs::create_dir_all(&path);
    Ok(path.to_string_lossy().to_string())
}

/// Lists all texture image files (.png, .jpg, .jpeg, .webp) in the user's local textures directory
#[tauri::command]
fn list_local_textures() -> Result<Vec<String>, String> {
    let dir_str = get_textures_dir()?;
    let dir = PathBuf::from(dir_str);
    let mut files = Vec::new();
    if let Ok(entries) = fs::read_dir(dir) {
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_file() {
                if let Some(ext) = path.extension().and_then(|s| s.to_str()) {
                    let ext_lower = ext.to_lowercase();
                    if ext_lower == "png" || ext_lower == "jpg" || ext_lower == "jpeg" || ext_lower == "webp" {
                        if let Some(name) = path.file_name().and_then(|s| s.to_str()) {
                            files.push(name.to_string());
                        }
                    }
                }
            }
        }
    }
    files.sort();
    Ok(files)
}

/// Reads a texture file from user's Textures directory and returns base64 DataURL
#[tauri::command]
fn read_local_texture_data_url(file_name: String) -> Result<String, String> {
    let dir_str = get_textures_dir()?;
    let path = PathBuf::from(dir_str).join(&file_name);
    if !path.exists() {
        return Err(format!("File not found: {}", file_name));
    }
    let ext = path.extension()
        .and_then(|s| s.to_str())
        .unwrap_or("png")
        .to_lowercase();
    let mime = match ext.as_str() {
        "jpg" | "jpeg" => "image/jpeg",
        "webp" => "image/webp",
        _ => "image/png",
    };
    let bytes = fs::read(&path).map_err(|e| e.to_string())?;
    let b64 = base64::engine::general_purpose::STANDARD.encode(&bytes);
    Ok(format!("data:{};base64,{}", mime, b64))
}

/// Imports an image into user's Textures directory from a base64 DataURL or raw base64
#[tauri::command]
fn import_texture_to_folder(file_name: String, base64_data: String) -> Result<String, String> {
    let dir_str = get_textures_dir()?;
    let path = PathBuf::from(&dir_str).join(&file_name);
    let pure_b64 = if let Some(idx) = base64_data.find(";base64,") {
        &base64_data[(idx + 8)..]
    } else {
        &base64_data
    };
    let bytes = base64::engine::general_purpose::STANDARD.decode(pure_b64.trim())
        .map_err(|e| e.to_string())?;
    fs::write(&path, bytes).map_err(|e| e.to_string())?;
    Ok(file_name)
}

/// Opens the textures folder in Windows Explorer / OS file manager
#[tauri::command]
fn open_textures_folder() -> Result<String, String> {
    let dir = get_textures_dir()?;
    #[cfg(target_os = "windows")]
    {
        let _ = std::process::Command::new("explorer").arg(&dir).spawn();
    }
    #[cfg(target_os = "macos")]
    {
        let _ = std::process::Command::new("open").arg(&dir).spawn();
    }
    #[cfg(target_os = "linux")]
    {
        let _ = std::process::Command::new("xdg-open").arg(&dir).spawn();
    }
    Ok(dir)
}

/// Saves any file (e.g. Godot .tscn, GLTF, OBJ, or procedural recipe) directly to disk
#[tauri::command]
fn export_to_disk(file_path: String, content: String) -> Result<bool, String> {
    if let Some(parent) = std::path::Path::new(&file_path).parent() {
        let _ = fs::create_dir_all(parent);
    }
    fs::write(&file_path, content).map_err(|e| e.to_string())?;
    Ok(true)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_fs::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            get_textures_dir,
            list_local_textures,
            read_local_texture_data_url,
            import_texture_to_folder,
            open_textures_folder,
            export_to_disk
        ])
        .run(tauri::generate_context!())
        .expect("error while running ModelCoder desktop application");
}
