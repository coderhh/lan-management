import { LanService } from '../service/lan.service';
import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { ActivatedRoute } from '@angular/router';
import { first } from 'rxjs/operators';
import { AlertService } from '../service/alert.service';
import { MacIpBind } from '../models/bind';

@Component({
  selector: 'app-vlan',
  templateUrl: './vlan.component.html',
  styleUrls: ['./vlan.component.scss']
})
export class VlanComponent implements OnInit, AfterViewInit {
  displayedColumns: string[] = ['id', 'vlan', 'mac', 'ip', 'mask', 'action'];

  title = 'LAN';
  vlanNum = '10';
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
    private alertService: AlertService
  ) {}

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
  ngOnInit(): void {
    this.route.params.forEach((params) => {
      this.vlanNum = params.id;
      this.loadvlaninfo();
    });
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  deleteBind(id: string): void {
    this.lanService.deleteBind(id).subscribe(
      (): void => {
        this.alertService.success('Deleted successful');
        window.location.reload();
      },
      (err) => {
        this.alertService.error(err);
      }
    );
  }

  deleteAllBindFromDB(): void {
    this.lanService.deleteAllBindFromDB().subscribe(
      (): void => {
        window.location.reload();
      },
      (err) => {
        this.alertService.error(err);
      }
    );
  }

  private loadvlaninfo(): void {
    this.lanService
      .getVlanBinds()
      .pipe(first())
      .subscribe((res) => {
        this.static_bind = res;
        this.dataSource.data = this.static_bind;
      });
  }
}
