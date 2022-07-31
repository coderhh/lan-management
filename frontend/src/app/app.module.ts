import { BrowserModule } from '@angular/platform-browser';
import { APP_INITIALIZER, NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatOptionModule } from '@angular/material/core';
import { MatDividerModule } from '@angular/material/divider';
import { ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LanService } from './service/lan.service';
import { HomeComponent } from './home/home.component';
import { VlanComponent } from './vlan/vlan.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FirewallComponent } from './firewall/firewall.component';
import { LoginComponent } from './login/login.component';
import { AlertComponent } from './alert/alert.component';
import { ErrorInterceptor } from './helpers/error.interceptor';
import { AdminComponent } from './admin/admin.component';
import { AccountsListComponent } from './accounts-list/accounts-list.component';
import { JwtInterceptor } from './helpers/jwt.interceptor';
import { AccountsAddEditComponent } from './accounts-add-edit/accounts-add-edit.component';
import { AccountService } from './service/account.service';
import { appInitializer } from './helpers/app.initializer';
import { FirewallAddEditComponent } from './firewall-add-edit/firewall-add-edit.component';
import { BindAddEditComponent } from './bind-add-edit/bind-add-edit.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    VlanComponent,
    FirewallComponent,
    LoginComponent,
    AlertComponent,
    AdminComponent,
    AccountsListComponent,
    AccountsAddEditComponent,
    FirewallAddEditComponent,
    BindAddEditComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatPaginatorModule,
    MatSortModule,
    MatCardModule,
    MatOptionModule,
    MatProgressSpinnerModule,
    MatTableModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule,
    MatSelectModule,
    MatDividerModule
  ],
  providers: [
    { provide: LanService, useClass: LanService },
    { provide: APP_INITIALIZER, useFactory: appInitializer, multi: true, deps: [AccountService] },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
