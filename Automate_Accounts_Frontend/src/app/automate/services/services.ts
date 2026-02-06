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
    const id = Date.now() + '-' + Math.floor(Math.random() * 100000);
    const file_name = this.file.name;
    const request = {
      "id": id,
      "file_name": file_name,
    }
    this.backendService.uploadFile(request).subscribe((response)=>{
      this.validate = true;
      this.fileId = id;
      this.fileName = file_name;
    })
  }

  validateFile(): void {
    const request = {
      "id": this.fileId,
      "file_name": this.fileName
    }
    console.log(request)
    this.backendService.validateFile(request).subscribe((response)=> {

    })
  }

  resetForm(): void{
    this.automateAccountForm.reset();
  }
}
