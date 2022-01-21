import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { LanService } from '../service/lan.service';
import { FireWallRule } from '../vlan/firewallrule';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-firewall',
  templateUrl: './firewall.component.html',
  styleUrls: ['./firewall.component.scss']
})
export class FirewallComponent implements OnInit, AfterViewInit {
  res: any;
  rules: FireWallRule[] = [];

  lanSubs: Subscription = new Subscription();

  displayedColumns: string[] = ['rule_num', 'ip', 'action'];
  dataSource = new MatTableDataSource<FireWallRule>();
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  constructor(public lanService: LanService, private router: Router) {

  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  ngOnInit(): void {
    this.load();
  }

  load(): void {
      this.lanService.getFireWallRules()
        .pipe(first())
        .subscribe(rules => {
          this.rules = rules;
          this.dataSource.data = this.rules;
        });
  }

  deleteRule(ruleNum: string) {
    // this.isLoadingResults = true;
    this.lanService.deleteRule(ruleNum)
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
  editRule(ruleNum: string){
    let editUrl = 'edit/'+ ruleNum;
    this.router.navigateByUrl(editUrl);
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
