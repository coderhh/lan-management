import { Component, OnInit } from '@angular/core';
import { AccountService } from '../service/account.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  isLoggedIn: boolean = false;
  constructor(private accountService: AccountService) { }

  ngOnInit(): void {
      const account = this.accountService.accountValue;
      if(account){
        this.isLoggedIn = true;
      }
  }

  logout(){
    this.accountService.logout();
    //window.location.reload();
  }
}
