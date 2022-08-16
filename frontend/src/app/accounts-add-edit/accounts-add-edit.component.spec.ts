import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FormBuilder } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { AccountService } from '../service/account.service';
import { AlertService } from '../service/alert.service';

import { AccountsAddEditComponent } from './accounts-add-edit.component';

describe('AccountsAddEditComponent', () => {
  let component: AccountsAddEditComponent;
  let fixture: ComponentFixture<AccountsAddEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [AccountsAddEditComponent],
      providers: [
        FormBuilder,
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: { params: { id: '24fkzrw3487943uf358lovd' } }
          }
        },
        AccountService,
        AlertService
      ]
    }).compileComponents();
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
