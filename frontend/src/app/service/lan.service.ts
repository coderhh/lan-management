import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, finalize, map } from 'rxjs/operators';
import { FireWallRule } from '../models/firewallrule';
import { environment } from '../../environments/environment';
import { MacIpBind } from '../models/bind';


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
    .pipe(finalize(() => {
      catchError(LanService._handleError)
    }));
  }

  getVlanBinds(){
    return this.http.get<MacIpBind[]>(`${baseUrl}/vlan`);
  }

  getVlanBindById(id: string) {
    return this.http.get<MacIpBind>(`${baseUrl}/vlan/${id}`);
  }

  createBind(bind: object){
    return this.http.post(`${baseUrl}/vlan`, bind);
  }

  updateBind(bindId: string, params: object){
    return this.http.put(`${baseUrl}/vlan/${bindId}`, params)
      .pipe(map((rule: any) => {
        return rule;
      }));
  }

  deleteBind(bindId: string) {
    return this.http.delete(`${baseUrl}/vlan/${bindId}`);
  }
}
