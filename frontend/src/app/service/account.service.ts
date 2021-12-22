import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { Account } from '../models/account';
import { environment } from '../../environments/environment';
import { map } from 'rxjs/operators';

const baseUrl = `${environment.apiUrl}`;
@Injectable({
  providedIn: 'root'
})
export class AccountService {
  logout() {
    throw new Error("Method not implemented.");
  }

  constructor(private http: HttpClient, router: Router) {
    this.accountSubject = new BehaviorSubject<Account>(new Account);
    this.account = this.accountSubject.asObservable();
  }

  public get accountValue(): Account {
    return this.accountSubject.value;
  }
  private accountSubject: BehaviorSubject<Account>;
  private account: Observable<Account>;

  private refreshTokenTimeout: any;

  login(email: string, password: string) {
    return this.http.post<any>(`${baseUrl}/authenticate`, {email, password}, { withCredentials: true})
          .pipe(map(account => {
            this.accountSubject.next(account);
            this.startRefreshTokenTimer();
            return account;
          }));
  }

  refreshToken() {
    return this.http.post<any>(`${baseUrl}/refresh-token`, {}, { withCredentials: true})
        .pipe(map((account) => {
          this.accountSubject.next(account);
          this.startRefreshTokenTimer();
          return account;
        }));
  }
  private startRefreshTokenTimer() {
    // parse json object from base64 encoded jwt token
    const jwtTokenEncoded = this.accountValue?.jwtToken;
    if (jwtTokenEncoded){
      const jwtToken = JSON.parse(atob(jwtTokenEncoded.split('.')[1]));
       // set a timeout to refresh the token a minute before it expires
      const expires = new Date(jwtToken.exp * 1000);
      const timeout = expires.getTime() - Date.now() - (60 * 1000);
      this.refreshTokenTimeout = setTimeout(() => this.refreshToken().subscribe(), timeout);
    }
  }
}
