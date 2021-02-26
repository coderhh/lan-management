import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewBindComponent } from './new-bind.component';

describe('NewBindComponent', () => {
  let component: NewBindComponent;
  let fixture: ComponentFixture<NewBindComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NewBindComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NewBindComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
