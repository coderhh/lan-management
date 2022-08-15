import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
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
  constructor(private http: HttpClient) {}

  private static _handleError(
    err: HttpErrorResponse | never
  ): Observable<never> {
    return Observable.throw(
      err.message || 'Error: Unable to complete request.'
    );
  }

  getFireWallRules(): Observable<FireWallRule[]> {
    return this.http.get<FireWallRule[]>(`${baseUrl}/firewallrule/`);
  }

  getRuleById(id: string): Observable<FireWallRule> {
    return this.http.get<FireWallRule>(`${baseUrl}/firewallrule/${id}`);
  }

  createRule(rule: object): Observable<unknown> {
    return this.http.post(`${baseUrl}/firewallrule/`, rule);
  }
  updateRule(ruleNum: string, params: object): Observable<FireWallRule> {
    return this.http
      .put<FireWallRule>(`${baseUrl}/firewallrule/${ruleNum}`, params)
      .pipe(map((rule: FireWallRule) => rule));
  }
  deleteRule(ruleNum: string): Observable<unknown> {
    return this.http.delete(`${baseUrl}/firewallrule/${ruleNum}`).pipe(
      finalize(() => {
        catchError(LanService._handleError);
      })
    );
  }

  deleteAllRulesFromDB(): Observable<unknown> {
    return this.http.delete(`${baseUrl}/firewallrule/`).pipe(
      finalize(() => {
        catchError(LanService._handleError);
      })
    );
  }

  getVlanBinds(): Observable<MacIpBind[]> {
    return this.http.get<MacIpBind[]>(`${baseUrl}/vlanbinding/`);
  }

  getVlanBindById(id: string): Observable<MacIpBind> {
    return this.http.get<MacIpBind>(`${baseUrl}/vlanbinding/${id}`);
  }

  createBind(bind: object): Observable<unknown> {
    return this.http.post(`${baseUrl}/vlanbinding/`, bind);
  }

  updateBind(bindId: string, params: object): Observable<MacIpBind> {
    return this.http
      .put<MacIpBind>(`${baseUrl}/vlanbinding/${bindId}`, params)
      .pipe(map((bind: MacIpBind) => bind));
  }

  deleteBind(bindId: string): Observable<unknown> {
    return this.http.delete(`${baseUrl}/vlanbinding/${bindId}`);
  }

  deleteAllBindFromDB(): Observable<unknown> {
    return this.http.delete(`${baseUrl}/vlanbinding/`).pipe(
      finalize(() => {
        catchError(LanService._handleError);
      })
    );
  }
}
