import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BackendService {
  private baseUrl = 'http://127.0.0.1:5000';

  constructor(private httpClient: HttpClient){}

 uploadFile(formData: FormData): Observable<any> {
  return this.httpClient.post(`${this.baseUrl}/upload`, formData);
}


  validateFile(request: any): Observable<any> {
    return this.httpClient.post(`${this.baseUrl}/validate`, request);
  }

  process(request: any): Observable<any> {
    return this.httpClient.post(`${this.baseUrl}/process`, request);
  }

getReceipts(): Observable<any[]> {
  return this.httpClient.get<any[]>(`${this.baseUrl}/receipts`);
}


getReceiptById(id: string): Observable<any> {
  return this.httpClient.get<any>(`${this.baseUrl}/receipts/${id}`);
}

}
