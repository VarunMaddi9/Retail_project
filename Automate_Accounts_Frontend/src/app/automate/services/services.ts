import { Component } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { BackendService } from '../../backend-service';

@Component({
  selector: 'app-services',
  standalone: false,
  templateUrl: './services.html',
  styleUrl: './services.css',
})
export class Services {

  automateAccountForm: FormGroup;
  file: File;
  fileName: string;
  validate: boolean;
  fileId: string;
  constructor(private formBuilder: FormBuilder, private backendService: BackendService){
    this.validate = false;
  }

  ngOnInit(): void {
  }

  async upload(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;
      if (!input.files || input.files.length === 0) {
        return;
      }

    this.file = input.files[0];
  }

submitAccountValidateForm(): void {
  if (!this.file) {
    alert('Please select a file before submitting');
    return;
  }

  const id = Date.now() + '-' + Math.floor(Math.random() * 100000);
  
  // Create FormData instead of JSON
  const formData = new FormData();
  formData.append('id', id);                   // metadata
  formData.append('file', this.file, this.file.name); // actual file

  // Send FormData
  this.backendService.uploadFile(formData).subscribe({
    next: (response) => {
      this.validate = true;
      this.fileId = id;
      this.fileName = this.file.name;
      console.log('Upload successful', response);
    },
    error: (error) => {
      console.error('Upload failed', error);
      alert('File upload failed');
    }
  });
}



  validateFile(): void {
    const request = {
      "id": this.fileId,
      "file_name": this.fileName
    }
    this.backendService.validateFile(request).subscribe((response)=> {
      console.log(response)
    })
  }

  resetForm(): void{
    this.automateAccountForm.reset();
  }
}
