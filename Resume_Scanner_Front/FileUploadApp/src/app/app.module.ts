import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { FileUploadComponent } from './file-upload/file-upload.component';
import { ApiResultComponent } from './api-result/api-result.component';

const routes: Routes = [
  { path: '', component: FileUploadComponent },
  { path: 'result', component: ApiResultComponent },
];

@NgModule({
  declarations: [AppComponent, FileUploadComponent, ApiResultComponent],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(routes),
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
