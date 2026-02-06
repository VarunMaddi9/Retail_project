import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AutomateRoutingModule } from './automate-routing-module';
import { Services } from './services/services';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    Services
  ],
  imports: [
    CommonModule,
    AutomateRoutingModule,
    ReactiveFormsModule,
    FormsModule
  ]
})
export class AutomateModule { }
