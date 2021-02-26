import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { LanService } from '../service/lan.service';

@Component({
  selector: 'app-new-rule',
  templateUrl: './new-rule.component.html',
  styleUrls: ['./new-rule.component.scss']
})
export class NewRuleComponent implements OnInit {

  newRuleForm: FormGroup;
  rule_numRegx = '^[0-9]+$';
  ip_addressRegx = '^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$';

  constructor(private formBuilder: FormBuilder, private lanService: LanService, private router: Router) {
    this.newRuleForm = this.formBuilder.group({
      rule_num: [null, [Validators.required, Validators.pattern(this.rule_numRegx)]],
      ip_address: [null, [Validators.required, Validators.pattern(this.ip_addressRegx)]]
    });
  }

  ngOnInit(): void {
  }

  submit() {
    if (!this.newRuleForm.valid) {
      return;
    }
    this.lanService.addNewRule(this.newRuleForm.value)
    .subscribe(
      response => {
        console.log(response);
        this.router.navigate(['/firewall/']);
      },
      console.error
    );
  }
}
