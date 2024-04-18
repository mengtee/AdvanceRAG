"use client"

import axios from 'axios';
import React, { useState, useEffect } from 'react';

interface FileSelectorProps {
  backendUrl: string;
}

const FileSelector: React.FC<FileSelectorProps> = ({ backendUrl }) => {
    const [selectedFile, setSelectedFile] = useState('');
    const [files, setFiles] = useState<string[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchFiles = async () => {
            setIsLoading(true);
            try {
                const response = await axios.get(`${backendUrl}/files/`);
                setFiles(response.data);
                setIsLoading(false);
            } catch (error) {
                console.error('Failed to fetch files:', error);
                setIsLoading(false);
                alert('Failed to load files');
            }
        };

        fetchFiles();
    }, [backendUrl]);

    const handleFileChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedFile(event.target.value);
    };

    const handleFileSubmit = async () => {
        if (!selectedFile) {
            alert("Please select a file first!");
            return;
        }

        try {
            const response = await axios.post(`${backendUrl}/process-file/`, { file_name: selectedFile });
            alert(`File processed: ${selectedFile}\nResponse: ${response.data.message}`);
        } catch (error) {
            console.error('Error processing file:', error);
            alert('Failed to process file');
        }
    };

    return (
        <div className="mt-4">
            <label htmlFor="file-selector" className="block text-sm font-medium text-gray-700">Select a file:</label>
            <select id="file-selector" onChange={handleFileChange} value={selectedFile} className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                <option value="">Select a file</option>
                {isLoading ? <option>Loading files...</option> : files.map((file, index) => (
                    <option key={index} value={file}>{file}</option>
                ))}
            </select>
            <button className="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500" onClick={handleFileSubmit}>
                Submit
            </button>
        </div>
    );
};

export default FileSelector;
