import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { first } from 'rxjs/operators';
import { MustMatch } from '../helpers/must-match';
import { Role, RoleInterface } from '../models/role';
import { AccountService } from '../service/account.service';
import { AlertService } from '../service/alert.service';

@Component({
  selector: 'app-accounts-add-edit',
  templateUrl: './accounts-add-edit.component.html',
  styleUrls: ['./accounts-add-edit.component.scss']
})
export class AccountsAddEditComponent implements OnInit {
  addEditForm!: FormGroup;
  id!:string;
  isAddMode!: boolean;
  loading: boolean = false;
  submitted: boolean = false;
  roles!: RoleInterface[];
  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private accountService: AccountService,
    private alertService: AlertService
  ) { }

  ngOnInit() {
    this.id = this.route.snapshot.params['id'];
    this.isAddMode = !this.id;

    this.addEditForm = this.formBuilder.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      role:['', Validators.required],
      password:['',[Validators.minLength(6), this.isAddMode ? Validators.required: Validators.nullValidator]],
      confirmPassword: ['']
    }, {
      validator: MustMatch('password', 'confirmPassword')
    });
    this.roles = [
      { value: 'User', viewValue: Role.User },
      { value: 'Admin', viewValue: Role.Admin }
    ];

    if(!this.isAddMode) {
      this.accountService.getById(this.id)
        .pipe(first())
        .subscribe(x => this.addEditForm.patchValue(x));
    }
  }

  get f() { return this.addEditForm.controls; }

  onSubmit() {
    this.submitted = true;

    this.alertService.clear();

    if (this.addEditForm.invalid) {
      return;
    }
    this.loading = true;
    if(this.isAddMode) {
      this.createAccount();
    } else {
      this.updateAccount();
    }
  }
  updateAccount(){
    this.accountService.update(this.id, this.addEditForm.value)
      .pipe(first())
      .subscribe({
        next: () => {
          this.alertService.success('Update successful', { keepAfterRouteChange: true});
          this.router.navigate(['../../'], { relativeTo: this.route });
        },
        error: error => {
          this.alertService.error(error);
          this.loading = false;
        }
      });
  }

  createAccount() {
    this.accountService.create(this.addEditForm.value)
      .pipe(first())
      .subscribe({
        next: () => {
          this.alertService.success('Account created successfully', { keepAfterRouteChange: true});
          this.router.navigate(['../'], { relativeTo: this.route});
        },
        error: error => {
          this.alertService.error(error);
          this.loading = false;
        }
      });
  }
}
