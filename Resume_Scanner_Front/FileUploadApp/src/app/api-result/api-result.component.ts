//import { Component } from '@angular/core';
import { Component, Input } from '@angular/core';


@Component({
  selector: 'app-api-result',
  templateUrl: './api-result.component.html',
})
export class ApiResultComponent {
  @Input() apiResponse: any;
}
