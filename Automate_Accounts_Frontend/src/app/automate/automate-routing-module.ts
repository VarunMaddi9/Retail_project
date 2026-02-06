import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Services } from './services/services';

const routes: Routes = [
  {path: '', redirectTo: 'automate', pathMatch: 'full'},
  { path: 'automate', component: Services}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AutomateRoutingModule { }
