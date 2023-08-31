import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
})
export class FileUploadComponent {
  cvFile: File | undefined;
  idFile: File | undefined;

  constructor(private http: HttpClient) {}

  onFileSelected(event: any, fileType: string) {
    const file = event.target.files[0];
    if (fileType === 'cv') {
      this.cvFile = file;
    } else if (fileType === 'id') {
      this.idFile = file;
    }
  }

  onSubmit(uploadForm: any) {
    const formData = new FormData();
  
    if (this.cvFile) {
      formData.append('cv_file', this.cvFile as Blob, this.cvFile.name);
    }
  
    if (this.idFile) {
      formData.append('id_file', this.idFile as Blob, this.idFile.name);
    }
  
    this.http.post('http://localhost:9091/check_cv', formData).subscribe(
      (response) => {
        console.log(response);
        
        // Navigate to result display component and pass response data
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }
}
