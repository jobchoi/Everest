import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module'; // AppRoutingModule을 임포트합니다.
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { MainPageComponent } from './components/main-page/main-page.component';
import { FooterComponent } from './components/footer/footer.component';

@NgModule({
  declarations: [],
  imports: [BrowserModule, AppRoutingModule, FooterComponent, HeaderComponent],
  providers: [],
  bootstrap: [],
})
export class AppModule {}
