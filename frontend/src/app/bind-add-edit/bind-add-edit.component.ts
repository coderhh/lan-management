import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { first } from 'rxjs/operators';
import { AlertService } from '../service/alert.service';
import { LanService } from '../service/lan.service';

const IP_ADDRESSREGX= '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$';
const VLANREGX = '^[0-9]*$';
@Component({
  selector: 'app-bind-add-edit',
  templateUrl: './bind-add-edit.component.html',
  styleUrls: ['./bind-add-edit.component.scss']
})
export class BindAddEditComponent implements OnInit {
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
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.id = this.route.snapshot.params['id'];
    this.isAddMode = !this.id;
    this.addEditForm = this.formBuilder.group({
      vlan_id: ['', [Validators.required, Validators.pattern(VLANREGX)]],
      mac_address: ['', [Validators.required]],
      ip_address: ['', [Validators.required, Validators.pattern(IP_ADDRESSREGX)]],
      network_mask: ['', [Validators.required, Validators.pattern(IP_ADDRESSREGX)]]
    });

    if(!this.isAddMode) {
      this.lanService.getVlanBindById(this.id)
        .pipe(first())
        .subscribe(bind => {
          this.addEditForm.patchValue(bind)
        });
    }
  }

  get f() { return this.addEditForm.controls;}

  onSubmit(){
    this.submitted = true;

    this.alertService.clear();
    if(this.addEditForm.invalid)
    {
      return;
    }

    this.loading = true;

    if (this.isAddMode){
      this.createBind();
    }else
    {
      this.updateBind();
    }
  }

  createBind() {
    this.lanService.createBind(this.addEditForm.value)
      .pipe(first())
      .subscribe({
        next: () => {
          this.alertService.success('New Bind created successfully', { keepAfterRouteChange: true});
          this.router.navigate(['../'], { relativeTo: this.route});;
        },
        error: error => {
          this.alertService.error(error);
          this.loading = false;
        }
      });
  }
  updateBind() {
    this.lanService.updateBind(this.id, this.addEditForm.value)
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
