/*    
	  This program is free software; you can redistribute it and/or modify
	  it under the terms of the GNU General Public License as published by
      the Free Software Foundation; either version 2 of the License, or
      (at your option) any later version.
      
      This program is distributed in the hope that it will be useful,
      but WITHOUT ANY WARRANTY; without even the implied warranty of
      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
      GNU General Public License for more details.
      
      You should have received a copy of the GNU General Public License
      along with this program; if not, write to the Free Software
      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
      MA 02110-1301, USA.
       
      Copyright 2010 Hiram Jeronimo Perez <worg@linuxmail.org>
*/

//This function does the magic of transofrming external links to pictures inside a plurk, into real pictures

function exImg() {
	imgs = document.getElementsByClassName('pictureservices'); // Get the pictureservices elements [external pictures in plurks] 
	j = imgs.length;
	for (i = 0;i < j;i++) //For every element in the array...
	{
		source = imgs[i];
		content = source.innerHTML;
		source.innerHTML = ''; //remove the inner text
		
		img= document.createElement("img"); //Create an IMG element
		
		img.setAttribute('src',content); //Add the old inner content 
		img.setAttribute('class', 'servImg'); 
		
		source.appendChild(img); //Add the IMG to the A element
	}
 }
