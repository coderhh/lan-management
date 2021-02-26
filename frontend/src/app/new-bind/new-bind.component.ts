import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LanService } from '../service/lan.service';

@Component({
  selector: 'app-new-bind',
  templateUrl: './new-bind.component.html',
  styleUrls: ['./new-bind.component.scss']
})
export class NewBindComponent implements OnInit {
  newBindForm: FormGroup;
  ip_addressRegx = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$';
  vlanRegx = '^[0-9]*$';
  constructor(private formBuilder: FormBuilder,
              private lanService: LanService,
              private router: Router) {
    this.newBindForm = this.formBuilder.group({
      vlan: [null, [Validators.required, Validators.pattern(this.vlanRegx)]],
      mac_address: [null, [Validators.required]],
      ip_address: [null, [Validators.required, Validators.pattern(this.ip_addressRegx)]]
    });
  }

  ngOnInit(): void {

  }

  submit() {
    if (!this.newBindForm.valid) {
      return;
    }
    this.lanService.addNewBind(this.newBindForm.value)
    .subscribe(
      response => {
        console.log(response);
        this.router.navigate(['/vlan/' + this.newBindForm.value.vlan ]);
      },
      console.error
    );
  }
}
