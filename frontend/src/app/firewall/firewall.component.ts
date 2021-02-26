import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { LanService } from '../service/lan.service';
import { FireWallRule } from '../vlan/firewallrule';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { Subscription } from 'rxjs';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-firewall',
  templateUrl: './firewall.component.html',
  styleUrls: ['./firewall.component.scss']
})
export class FirewallComponent implements OnInit, AfterViewInit {
  res: any;
  rules: FireWallRule[] = [];

  lanSubs: Subscription;

  displayedColumns: string[] = ['rule_num', 'ip', 'action'];
  dataSource = new MatTableDataSource<FireWallRule>();
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  constructor(public _lanService: LanService, private router: Router) {

  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this._lanService.getFireWallRules()
      .subscribe(res => {
        this.res = res;
        for (const rule of this.res.rules) {
          this.rules.push({rule_num: rule.rule_num, ip_address: rule.ip_address});
        }
        this.dataSource.data = this.rules;
      },
      console.error
      );
  }

  deleteRule(ruleNum: any) {
    // this.isLoadingResults = true;
    this._lanService.deleteRule(ruleNum)
      .subscribe(res => {
          // this.isLoadingResults = false;
          console.log(res);
          window.location.reload();
        }, (err) => {
          console.log(err);
          // this.isLoadingResults = false;
        }
      );
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  ngOnDestroy() {
    if (this.lanSubs){
      this.lanSubs.unsubscribe();
    }
  }
}
