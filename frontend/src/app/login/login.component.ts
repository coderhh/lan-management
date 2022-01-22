import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { first } from 'rxjs/operators';
import { AccountService } from '../service/account.service';
import { AlertService } from '../service/alert.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  loading = false;
  submitted = false;
  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private accountService: AccountService,
    private alertService: AlertService
    ) { }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }
  get f() { return this.loginForm.controls; }

  onSubmit(){
    this.submitted = true;
    if (this.loginForm.invalid){
      return;
    }
    this.loading = true;
    this.accountService.login(this.f.email.value, this.f.password.value)
        .pipe(first())
        .subscribe({
          next: () => {
            const returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/home';
            this.router.navigateByUrl(returnUrl);
            //window.location.reload();
          },
          error: error => {
            this.alertService.error(error);
            this.loading = false;
          }
        });
  }

  getErrorMessage() {

  }

}
