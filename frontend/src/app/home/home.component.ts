import { Component, OnInit } from '@angular/core';
import { Account } from '../models/account';
import { Role } from '../models/role';
import { AccountService } from '../service/account.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  isLoggedIn = false;
  isAdmin = false;
  account!: Account;
  constructor(private accountService: AccountService) {
    this.accountService.account.subscribe((x) => (this.account = x));
  }

  ngOnInit(): void {
    if (this.account.public_id) {
      this.isLoggedIn = true;
      if (this.account.role?.toLocaleUpperCase() == Role.Admin) {
        this.isAdmin = true;
      }
    }
  }

  logout() {
    this.accountService.logout();
  }
}
