import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing-module';
import { App } from './navigation-components/app/app';
import { Navigation } from './navigation-components/navigation/navigation';
import { AutomateModule } from './automate/automate-module';

@NgModule({
  declarations: [
    App,
    Navigation
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AutomateModule
  ],
  providers: [
    provideBrowserGlobalErrorListeners(),
  ],
  bootstrap: [App]
})
export class AppModule { }
