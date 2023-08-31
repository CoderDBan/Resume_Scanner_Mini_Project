import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApiResultComponent } from './api-result.component';

describe('ApiResultComponent', () => {
  let component: ApiResultComponent;
  let fixture: ComponentFixture<ApiResultComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ApiResultComponent]
    });
    fixture = TestBed.createComponent(ApiResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
