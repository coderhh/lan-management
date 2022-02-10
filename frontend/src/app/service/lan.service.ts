import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse} from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError, finalize, map } from 'rxjs/operators';
import { FireWallRule } from '../models/firewallrule';
import { environment } from '../../environments/environment';
import { MacIpBind } from '../models/bind';

const baseUrl = `${environment.apiUrl}`;
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
     return this.http.get<FireWallRule[]>(`${baseUrl}/firewallrule/`);
  }

  getRuleById(id: string) {
    return this.http.get<FireWallRule>(`${baseUrl}/firewallrule/${id}`);
  }

  createRule(rule: object) {
    return this.http.post(`${baseUrl}/firewallrule/`, rule);
  }
  updateRule(ruleNum: string, params: object){
    return this.http.put(`${baseUrl}/firewallrule/${ruleNum}`, params)
      .pipe(map((rule: any) => {
        return rule;
      }));
  }
  deleteRule(ruleNum: string) {
    return this.http.delete(`${baseUrl}/firewallrule/${ruleNum}`)
    .pipe(finalize(() => {
      catchError(LanService._handleError)
    }));
  }

  getVlanBinds(){
    return this.http.get<MacIpBind[]>(`${baseUrl}/vlanbinding/`);
  }

  getVlanBindById(id: string) {
    return this.http.get<MacIpBind>(`${baseUrl}/vlanbinding/${id}`);
  }

  createBind(bind: object){
    return this.http.post(`${baseUrl}/vlanbinding/`, bind);
  }

  updateBind(bindId: string, params: object){
    return this.http.put(`${baseUrl}/vlanbinding/${bindId}`, params)
      .pipe(map((rule: any) => {
        return rule;
      }));
  }

  deleteBind(bindId: string) {
    return this.http.delete(`${baseUrl}/vlanbinding/${bindId}`);
  }
}
