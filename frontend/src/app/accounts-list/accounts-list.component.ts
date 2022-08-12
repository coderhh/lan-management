import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { first } from 'rxjs/operators';
import { Account } from '../models/account';
import { AlertOption } from '../models/AlertOption';
import { AccountService } from '../service/account.service';
import { AlertService } from '../service/alert.service';

@Component({
  selector: 'app-accounts-list',
  templateUrl: './accounts-list.component.html',
  styleUrls: ['./accounts-list.component.scss']
})
export class AccountsListComponent implements OnInit, AfterViewInit {
  accounts: Account[] = [];
  displayedColumns: string[] = [
    'lastName',
    'firstName',
    'email',
    'role',
    'action'
  ];
  dataSource = new MatTableDataSource<Account>();
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatTable) table!: MatTable<Account>;

  constructor(
    private accountService: AccountService,
    private alertService: AlertService
  ) {}
  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  ngOnInit() {
    this.accountService
      .getAll()
      .pipe(first())
      .subscribe((accounts) => {
        this.accounts = accounts;
        this.dataSource.data = this.accounts;
      });
  }

  deleteAccount(id: string) {
    this.accountService
      .delete(id)
      .pipe(first())
      .subscribe({
        next: () => {
          this.alertService.success(
            'Account deleted successfully',
            new AlertOption(true)
          );
          this.accounts = this.accounts.filter((x) => x.public_id !== id);
          window.location.reload();
        },
        error: (error) => {
          this.alertService.error(error);
        }
      });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
}
