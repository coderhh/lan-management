import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { first } from 'rxjs/operators';
import { AlertOption } from '../models/AlertOption';
import { AlertService } from '../service/alert.service';
import { LanService } from '../service/lan.service';

const ipAddressRegx = '^(?:[0-9]{1,3}.){3}[0-9]{1,3}$';
@Component({
  selector: 'app-firewall-add-edit',
  templateUrl: './firewall-add-edit.component.html',
  styleUrls: ['./firewall-add-edit.component.scss']
})
export class FirewallAddEditComponent implements OnInit {
  addEditForm!: FormGroup;
  id!: string;
  isAddMode!: boolean;
  loading = false;
  submitted = false;

  constructor(
    private formBuilder: FormBuilder,
    private lanService: LanService,
    private alertService: AlertService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.id = this.route.snapshot.params['id'];
    this.isAddMode = !this.id;

    this.addEditForm = this.formBuilder.group({
      ip_address: ['', [Validators.required, Validators.pattern(ipAddressRegx)]]
    });

    if (!this.isAddMode) {
      this.lanService
        .getRuleById(this.id)
        .pipe(first())
        .subscribe((rule) => {
          this.addEditForm.patchValue(rule);
          this.loading = false;
        });
    }
  }

  get f() {
    return this.addEditForm.controls;
  }

  submit() {
    this.submitted = true;

    this.alertService.clear();
    if (this.addEditForm.invalid) {
      return;
    }
    this.loading = true;

    if (this.isAddMode) {
      this.createRule();
    } else {
      this.updateRule();
    }
  }
  createRule() {
    this.lanService
      .createRule(this.addEditForm.value)
      .pipe(first())
      .subscribe({
        next: () => {
          this.alertService.success(
            'Rule created successfully',
            new AlertOption(true)
          );
          this.router.navigate(['../'], { relativeTo: this.route });
        },
        error: (error) => {
          this.alertService.error(error);
          this.loading = false;
        }
      });
  }

  // method to update existing rule
  updateRule() {
    this.lanService
      .updateRule(this.id, this.addEditForm.value)
      .pipe(first())
      .subscribe({
        next: () => {
          this.alertService.success('Update successful', new AlertOption(true));
          this.router.navigate(['../../'], { relativeTo: this.route });
        },
        error: (error) => {
          this.alertService.error(error);
          this.loading = false;
        }
      });
  }
}
