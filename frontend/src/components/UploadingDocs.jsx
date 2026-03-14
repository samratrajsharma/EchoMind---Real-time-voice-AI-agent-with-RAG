import { useState } from "react";
import axios from "axios";

function UploadDocs() {
  const [file, setFile] = useState(null);

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    await axios.post(
      "http://127.0.0.1:8000/upload",
      formData
    );

    alert("Document uploaded!");
  };

  return (
    <div>
      <h3>Upload Document</h3>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadFile}>
        Upload
      </button>
    </div>
  );
}

export default UploadDocs;