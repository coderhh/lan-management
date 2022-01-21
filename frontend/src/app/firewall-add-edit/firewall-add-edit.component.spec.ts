import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FirewallAddEditComponent } from './firewall-add-edit.component';

describe('FirewallAddEditComponent', () => {
  let component: FirewallAddEditComponent;
  let fixture: ComponentFixture<FirewallAddEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FirewallAddEditComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FirewallAddEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
