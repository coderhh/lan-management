import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Route, Router } from '@angular/router';
import { first } from 'rxjs/operators';
import { AlertService } from '../service/alert.service';
import { LanService } from '../service/lan.service';

const rule_numRegx = '^[0-9]+$';
const ip_addressRegx = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$';
@Component({
  selector: 'app-firewall-add-edit',
  templateUrl: './firewall-add-edit.component.html',
  styleUrls: ['./firewall-add-edit.component.scss']
})
export class FirewallAddEditComponent implements OnInit {
  addEditForm!: FormGroup;
  id!: string;
  isAddMode!: boolean;
  loading: boolean = false;
  submitted: boolean = false;

  constructor(
    private formBuilder: FormBuilder,
    private lanService: LanService,
    private alertService: AlertService,
    private router: Router,
    private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.id = this.route.snapshot.params['id'];
    this.isAddMode = !this.id;

    this.addEditForm = this.formBuilder.group({
      rule_num: ['', [Validators.required, Validators.pattern(rule_numRegx)]],
      ip_address: ['', [Validators.required, Validators.pattern(ip_addressRegx)]]
    });

    if(!this.isAddMode){
      this.lanService.getRuleById(this.id)
        .pipe(first())
        .subscribe(rule => {
          this.addEditForm.patchValue(rule);
          this.loading = false;
        });
    }
  }

  get f() { return this.addEditForm.controls;}

  submit() {
    this.submitted = true;

    this.alertService.clear();
    if (this.addEditForm.invalid) {
      return;
    }
    this.loading = true;

    if(this.isAddMode){
      this.createRule();
    } else
    {
      this.updateRule();
    }
  }
  createRule() {
    this.lanService.createRule(this.addEditForm.value)
      .pipe(first())
      .subscribe({
        next: () => {
          this.alertService.success('Rule created successfully', { keepAfterRouteChange: true});
          this.router.navigate(['../'], { relativeTo: this.route});;
        },
        error: error => {
          this.alertService.error(error);
          this.loading = false;
        }
      });
  }

  // method to update existing rule
  updateRule() {
    this.lanService.updateRule(this.id, this.addEditForm.value)
      .pipe(first())
      .subscribe({
        next: () => {
          this.alertService.success('Update successful', { keepAfterRouteChange: true});
          this.router.navigate(['../../'], { relativeTo: this.route});
        },
        error: error => {
          this.alertService.error(error);
          this.loading = false;
        }
      });
  }
}