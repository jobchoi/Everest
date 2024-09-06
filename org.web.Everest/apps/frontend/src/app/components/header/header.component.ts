import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderInterface, HeaderMenuItem } from '../../header-interface';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {
  menuItems: HeaderMenuItem[] = [];

  private readonly menuData: HeaderInterface = {
    menuItems: [
      { menuMax: 1, menuName: 'Home', menuUrl: '/home' },
      { menuMax: 2, menuName: 'About', menuUrl: '/about' },
      { menuMax: 3, menuName: 'Services', menuUrl: '/services' },
      { menuMax: 3, menuName: 'Services', menuUrl: '/services' },
      { menuMax: 3, menuName: 'Services', menuUrl: '/services' },
      { menuMax: 3, menuName: 'Services', menuUrl: '/services' },
      { menuMax: 3, menuName: 'Services', menuUrl: '/services' },
    ],
  };

  ngOnInit(): void {
    this.menuItems = this.menuData.menuItems;
  }
}
