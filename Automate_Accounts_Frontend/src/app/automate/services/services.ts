import { Component } from '@angular/core';
import { FormGroup, FormBuilder } from '@angular/forms';
import { BackendService } from '../../backend-service';
import { ToastrService } from 'ngx-toastr';

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
  constructor(private formBuilder: FormBuilder, private backendService: BackendService, private toastr: ToastrService){
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
    this.toastr.warning("Please select a file before submitting")
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
      this.toastr.success("Upload successful")
      //console.log('Upload successful', response);
    },
    error: (error) => {
      this.toastr.error("File Upload Failed")
      console.error('Upload failed', error);

    }
  });
}



  validateFile(): void {
    const request = {
      "id": this.fileId,
      "file_name": this.fileName
    }
    this.backendService.validateFile(request).subscribe((response)=> {
      if(response.is_valid){
        this.toastr.success("Successful", "Validation")
      }
      else {
        this.toastr.error("not a valid PDF", "File is")
      }
    })
  }

  resetForm(): void{
    this.automateAccountForm.reset();
  }
}
