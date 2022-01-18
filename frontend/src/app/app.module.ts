import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
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
import { ReactiveFormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LanService } from './service/lan.service';
import { HomeComponent } from './home/home.component';
import { VlanComponent } from './vlan/vlan.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FirewallComponent } from './firewall/firewall.component';
import { NewRuleComponent } from './new-rule/new-rule.component';
import { NewBindComponent } from './new-bind/new-bind.component';
import { LoginComponent } from './login/login.component';
import { AlertComponent } from './alert/alert.component';
import { fakeBackendProvider } from './helpers/fake-backend.interceptor';
import { ErrorInterceptor } from './helpers/error.interceptor';



@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    VlanComponent,
    FirewallComponent,
    NewRuleComponent,
    NewBindComponent,
    LoginComponent,
    AlertComponent
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
    MatProgressSpinnerModule,
    MatTableModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule
  ],
  providers: [LanService,
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    fakeBackendProvider
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
