import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { BASE_API_URL } from '../env';
import { FireWallRule } from '../vlan/firewallrule';
import { Bind } from '../new-bind/bind';
import { environment } from '../../environments/environment';
import { MacIpBind } from '../vlan/vlan.component';

const baseUrl = `${environment.apiUrl}/lan`;
@Injectable({
  providedIn: 'root'
})

export class LanService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  // getVlan(vlanNum: string){
  //   return this.http.get(`${baseUrl}/vlan/${vlanNum}`);
  // }
  getVlan(){
    return this.http.get<MacIpBind[]>(`${baseUrl}/vlan`);
  }

  getFireWallRules() {
     return this.http.get<FireWallRule[]>(`${baseUrl}/firewall`);
  }

  getRuleById(id: string) {
    return this.http.get<FireWallRule>(`${baseUrl}/firewall/${id}`);
  }

  createRule(rule: object) {
    return this.http.post(`${baseUrl}/firewall`, rule);
  }
  updateRule(ruleNum: string, params: object){
    return this.http.put(`${baseUrl}/firewall/${ruleNum}`, params)
      .pipe(map((rule: any) => {
        return rule;
      }));
  }
  deleteRule(ruleNum: string) {
    return this.http.delete(`${baseUrl}/firewall/${ruleNum}`)
    .pipe(
      catchError(LanService._handleError)
    );
  }

  addNewBind(bind: Bind){
    return this.http
    .post(`${baseUrl}/lan/api/v1.0/vlan/add/`, bind)
    .pipe(
      catchError(LanService._handleError)
    );
  }

  deleteBind(bindId: string) {
    return this.http.delete(`${baseUrl}/vlan/${bindId}`);
  }
}
