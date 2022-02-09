import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable } from 'rxjs';
import { Account } from '../models/account';
import { environment } from '../../environments/environment';
import { finalize, map } from 'rxjs/operators';

const baseUrl = `${environment.apiUrl}/account`;
const authUrl = `${environment.apiUrl}/auth`;
@Injectable({
  providedIn: 'root'
})
export class AccountService {
  private accountSubject: BehaviorSubject<any>;
  public account: Observable<Account>;

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    this.accountSubject = new BehaviorSubject<any>(null);
    this.account = this.accountSubject.asObservable();
  }

  public get accountValue(): Account {
    return this.accountSubject.value;
  }


  login(email: string, password: string) {
    return this.http.post<any>(`${authUrl}/login`, {email, password}, { withCredentials: true})
          .pipe(map(account => {
            this.accountSubject.next(account);
            this.startRefreshTokenTimer();
            return account;
          }));
  }

  logout(){
    this.http.post<any>(`${authUrl}/logout`, {}, { withCredentials: true}).subscribe();
    this.stopRefreshTokenTimer();
    this.accountSubject.next(null);
    this.router.navigate(['/home']);
  }

  getAll(){
    return this.http.get<Account[]>(`${baseUrl}/`);
  }

  getById(id: string)
  {
    return this.http.get<Account>(`${baseUrl}/${id}`);
  }

  create(params: object)
  {
    return this.http.post(`${baseUrl}/`, params);
  }

  update(id:string, params: object)
  {
    return this.http.put(`${baseUrl}/${id}`, params)
        .pipe(map((account: any) => {
          if(account.id === this.accountValue.id)
          {
            account = { ...this.accountValue, ...account };
            this.accountSubject.next(account);
          }
          return account;
        }));
  }

  delete(id: string)
  {
    return this.http.delete(`${baseUrl}/${id}`)
        .pipe(finalize(() => {
          if(id === this.accountValue.id)
            this.logout();
        }));
  }


  refreshToken() {
    return this.http.post<any>(`${authUrl}/refresh-token`, {}, { withCredentials: true})
        .pipe(map((account) => {
          //console.log(account)
          this.accountSubject.next(account);
          this.startRefreshTokenTimer();
          return account;
        }));
  }

  private refreshTokenTimeout: any;
  stopRefreshTokenTimer() {
    clearTimeout(this.refreshTokenTimeout);
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
