import { Component, OnInit } from '@angular/core';
import { first } from 'rxjs/operators';
import { AccountService } from '../service/account.service';

@Component({
  selector: 'app-accounts-list',
  templateUrl: './accounts-list.component.html',
  styleUrls: ['./accounts-list.component.scss']
})
export class AccountsListComponent implements OnInit {
  accounts!: any[];
  displayedColumns: string[] = ['lastName', 'firstName', 'email', 'role', 'action'];
  constructor(private accountService:AccountService) { }

  ngOnInit() {
    this.accountService.getAll()
        .pipe(first())
        .subscribe(accounts => this.accounts = accounts)
  }

  deleteAccount(id: string){
    const account = this.accounts.find(x => x.id === id);
    account.isDeleting = true;
    this.accountService.delete(id)
        .pipe(first())
        .subscribe(() => {
          this.accounts = this.accounts.filter(x => x.id !== id )
        });
  }
}

