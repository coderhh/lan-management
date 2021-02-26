import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { BASE_API_URL } from '../env';
import { FireWallRule } from '../vlan/firewallrule';
import { Bind } from '../new-bind/bind';

@Injectable({
  providedIn: 'root'
})

export class LanService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  getVlan(vlanNum: string){
    return this.http
      .get(`${BASE_API_URL}/lan/api/v1.0/vlan/` + vlanNum)
      .pipe(
          catchError(LanService._handleError)
      );
  }

  getFireWallRules() {
     return this.http
     .get(`${BASE_API_URL}/lan/api/v1.0/firewall/`)
     .pipe(
        catchError(LanService._handleError)
     );
  }

  addNewRule(rule: FireWallRule) {
    return this.http
    .post(`${BASE_API_URL}/lan/api/v1.0/firewall/`, rule)
    .pipe(
      catchError(LanService._handleError)
    );
  }

  deleteRule(ruleNum: string) {
    return this.http
    .delete(`${BASE_API_URL}/lan/api/v1.0/firewall/delete/` +  ruleNum)
    .pipe(
      catchError(LanService._handleError)
    );
  }

  addNewBind(bind: Bind){
    return this.http
    .post(`${BASE_API_URL}/lan/api/v1.0/vlan/add/`, bind)
    .pipe(
      catchError(LanService._handleError)
    );
  }

  deleteBind(bind: Bind) {
    console.log(bind);
    return this.http
    .post(`${BASE_API_URL}/lan/api/v1.0/vlan/delete/`, bind)
    .pipe(
      catchError(LanService._handleError)
    );
  }
}
