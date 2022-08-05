import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AccountService } from '../service/account.service';
import { environment } from 'src/environments/environment';

@Injectable()
export class JwtInterceptor implements HttpInterceptor {
  constructor (private accountService: AccountService) { }

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const account = this.accountService.accountValue;
    const isLoggedIn = account && account.jwtToken;
    const isApiUrl = request.url.startsWith(environment.apiUrl);
    if (isLoggedIn && isApiUrl) {
      // const headers = new HttpHeaders({
      //   'Authorization': `Bear ${account.jwtToken}`,
      //   'RefreshToken': `${account.refreshToken}`
      // });
      // request = request.clone({headers});
      request = request.clone({
        setHeaders: { Authorization: `Bear ${account.jwtToken}` }
      });
    }
    return next.handle(request);
  }
}
