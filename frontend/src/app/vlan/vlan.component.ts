import { LanService } from '../service/lan.service';
import { Component, OnInit, AfterViewInit, ViewChild} from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { Subscription } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { Bind } from '../new-bind/bind';

export interface MacIpBind {
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

  lanSubs: Subscription;

  vlan: any;

  vlanNum: string;

  vlanName = '';

  network = '';
  mask = '';
  dns_list = [];
  gateway_list = [];

  static_bind: MacIpBind[] = [];


  dataSource = new MatTableDataSource<MacIpBind>();

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  constructor(private lanService: LanService, private route: ActivatedRoute) {
    this.lanSubs = new Subscription();
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }
  ngOnInit(): void {
    this.route.params.forEach(params => {
      this.vlanNum = params.id;
      console.log(this.vlanName);
      this.loadvlaninfo(this.vlanNum);
    });
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  deleteBind(ip: string ): void {
    console.log(this.vlanNum);
    console.log(ip);
    const bind: Bind = { vlan: this.vlanNum, ip_address: ip, mac_address: '' };

    this.lanService.deleteBind(bind)
    .subscribe(
      response => {
        console.log(response);
      },
      console.error
    );
  }

  ngOnDestroy(): void {
    this.lanSubs.unsubscribe();
  }

  private loadvlaninfo(num: string): void{
    this.lanSubs = this.lanService
      .getVlan(this.vlanNum)
      .subscribe(res => {
          this.vlan = res;
          this.vlanName = this.vlan.vlan_name;
          this.network = this.vlan.network;
          this.mask = this.vlan.mask;
          this.dns_list = this.vlan.dns_list;
          this.gateway_list = this.vlan.gateway_list;
          this.static_bind = [];
          for (const bind of this.vlan.static_bind) {
            this.static_bind.push({vlan: this.vlanName, mac: bind.mac_address, ip: bind.ip_address, mask: bind.mask });
          }

          this.dataSource.data = this.static_bind;
        },
        console.error
      );
  }

}
