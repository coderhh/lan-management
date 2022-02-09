import { Component, OnInit } from '@angular/core';
import { Account } from '../models/account';
import { AccountService } from '../service/account.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  isLoggedIn: boolean = false;
  account!: Account;
  constructor(private accountService: AccountService) {
    this.accountService.account.subscribe(x => this.account = x);
  }

  ngOnInit(): void {
      if(this.account){
        this.isLoggedIn = true;
      }
  }

  logout(){
    this.accountService.logout();
    //window.location.reload();
  }
}
