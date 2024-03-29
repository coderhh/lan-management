import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { LanService } from '../service/lan.service';
import { FireWallRule } from '../models/firewallrule';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { first } from 'rxjs/operators';
import { AlertService } from '../service/alert.service';
import { AlertOption } from '../models/AlertOption';

@Component({
  selector: 'app-firewall',
  templateUrl: './firewall.component.html',
  styleUrls: ['./firewall.component.scss']
})
export class FirewallComponent implements OnInit, AfterViewInit {
  rules: FireWallRule[] = [];
  displayedColumns: string[] = ['rule_num', 'ip', 'action'];
  dataSource: MatTableDataSource<FireWallRule> =
    new MatTableDataSource<FireWallRule>();
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatTable) table!: MatTable<FireWallRule>;
  constructor(
    public lanService: LanService,
    private alertService: AlertService
  ) {}

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  ngOnInit(): void {
    this.lanService
      .getFireWallRules()
      .pipe(first())
      .subscribe((rules) => {
        this.rules = rules;
        this.dataSource.data = this.rules;
      });
  }

  deleteRule(ruleNum: string): void {
    this.lanService
      .deleteRule(ruleNum)
      .pipe(first())
      .subscribe({
        next: () => {
          this.alertService.success(
            'Rule deleted successfully',
            new AlertOption(true)
          );
          this.rules.filter((x) => x.rule_num !== ruleNum);
          window.location.reload();
        },
        error: (error) => {
          this.alertService.error(error);
        }
      });
  }

  deleteAllRulesFromDB(): void {
    this.lanService
      .deleteAllRulesFromDB()
      .pipe(first())
      .subscribe({
        next: () => {
          window.location.reload();
        },
        error: (error) => {
          this.alertService.error(error);
        }
      });
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
}
