import { LanService } from '../service/lan.service';
import { Component, OnInit, AfterViewInit, ViewChild} from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { Subscription } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { Bind } from '../new-bind/bind';
import { first } from 'rxjs/operators';
import { AlertService } from '../service/alert.service';

export interface MacIpBind {
  id: string;
  vlan: string;
  ip: string;
  mac: string;
  mask: string;
}

@Component({
  selector: 'app-vlan',
  templateUrl: './vlan.component.html',
  styleUrls: ['./vlan.component.scss']
})
export class VlanComponent implements OnInit, AfterViewInit {

  displayedColumns: string[] = ['vlan', 'mac', 'ip', 'mask', 'action'];

  title = 'LAN';
  vlan: any;
  vlanNum: string = '10';
  vlanName = '';
  network = '';
  mask = '';
  dns_list = [];
  gateway_list = [];

  static_bind: MacIpBind[] = [];
  dataSource = new MatTableDataSource<MacIpBind>();

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private lanService: LanService,
    private route: ActivatedRoute,
    private alertService: AlertService) {
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
  ngOnInit(): void {
    this.route.params.forEach(params => {
      this.vlanNum = params.id;
      this.loadvlaninfo(this.vlanNum);
    });
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  deleteBind(id: string ): void {
    this.lanService.deleteBind(id)
    .subscribe(
      response => {
        this.alertService.success('Deleted successful');
        window.location.reload();
      }, (err) => {
        this.alertService.error(err);
      }
    );
  }

  ngOnDestroy(): void {

  }

  private loadvlaninfo(num: string): void{
    this.lanService.getVlan()
        .pipe(first())
        .subscribe(res => {
          this.static_bind = res;
          this.dataSource.data = this.static_bind;
        });
  }
}
