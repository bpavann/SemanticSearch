import React, { useState } from 'react';
import axios from 'axios';

function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [result, setResult] = useState("");

  const handleFileUpload = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    console.log("File submitted");
    const formData = new FormData();
    formData.append('file', selectedFile);
  
    try {
      const response = await axios.post('/', formData);
      setResult(response.data.result);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <React.Fragment>
      <div className="heading">
        <p className="head1">Semantic Search of Research Papers</p>
      </div>
              
      <div className="content">
        <div className="wrapper">
          <h2>You can add your PDF file here and get the relevant results</h2>
          <form onSubmit={handleSubmit}>
            <div className="addFile">
              <label htmlFor="file-upload" className="file-upload">
                <input className="file-upload__input" type="file" name="myFile[]" id="myFile" onChange={handleFileUpload} /><br/><br/>
                <div className='button'>
                  <button type="submit">Upload</button>
                </div>
              </label>
            </div>
          </form>

          <div className="result">{result}</div>
        </div>
      </div>
    </React.Fragment>
  );
}

export default Home;
