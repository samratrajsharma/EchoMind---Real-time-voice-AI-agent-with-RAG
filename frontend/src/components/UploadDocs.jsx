import axios from "axios"
import { useState } from "react"

function UploadDocs(){

    const [file,setFile] = useState(null)

    const upload = async () => {

        const form = new FormData()
        form.append("file",file)

        await axios.post(
            "http://127.0.0.1:8000/upload",
            form
        )

        alert("Document uploaded")
    }

    return(
        <div>

            <h3>Upload Knowledge Document</h3>

            <input
                type="file"
                onChange={(e)=>setFile(e.target.files[0])}
            />

            <button onClick={upload}>
                Upload
            </button>

        </div>
    )
}

export default UploadDocs