import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountsAddEditComponent } from './accounts-add-edit.component';

describe('AccountsAddEditComponent', () => {
  let component: AccountsAddEditComponent;
  let fixture: ComponentFixture<AccountsAddEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AccountsAddEditComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AccountsAddEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
