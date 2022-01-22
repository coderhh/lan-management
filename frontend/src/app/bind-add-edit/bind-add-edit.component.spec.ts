import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BindAddEditComponent } from './bind-add-edit.component';

describe('BindAddEditComponent', () => {
  let component: BindAddEditComponent;
  let fixture: ComponentFixture<BindAddEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BindAddEditComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BindAddEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
