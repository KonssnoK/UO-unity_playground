using System;
using System.IO;
using System.Text;
using System.Collections.Generic;

namespace Mythic.Package
{
	/// <summary>
	/// Handles .uop hashing.
	/// </summary>
	public static class HashDictionary
	{
		#region FileName
		private static string m_FileName = AppDomain.CurrentDomain.BaseDirectory + "Dictionary.dic";

		/// <summary>
		/// Default name of the dictionary.
		/// </summary>
		public static string FileName{ get{ return m_FileName; } }
		#endregion

		#region Modified
		private static bool m_Modified = false;

		/// <summary>
		/// Was this dictionary modified?
		/// </summary>
		public static bool Modified{ get{ return m_Modified; } }
		#endregion

		#region NewHashes
		private static int m_NewHashes;

		/// <summary>
		/// Number of new hashes since load. Resets upon save.
		/// </summary>
		public static int NewHashes{ get{ return m_NewHashes; } }
		#endregion

		#region NewFileNames
		private static int m_NewFileNames;
		
		/// <summary>
		/// Number of new file names since load. Resets upon save.
		/// </summary>
		public static int NewFileNames{ get{ return m_NewFileNames; } }
		#endregion

		#region Hashing
		/// <summary>
		/// Computes Adler32 hash of the <paramref name="d"/>.
		/// </summary>
		/// <param name="d">Data to hash.</param>
		/// <returns>Adler32 hash.</returns>
		public static uint HashDataBlock( byte[] d )
		{
			uint a = 1;
			uint b = 0;

			for ( int i = 0; i < d.Length; i++ )
			{
				a = ( a + d[ i ] ) % 0xFFF1;
				b = ( b + a ) % 0xFFF1;
			}

			return ( b << 16 ) | a;
		}

		/// <summary>
		/// Computes KR hash of the <paramref name="s"/>.
		/// </summary>
		/// <param name="s">String to hash.</param>
		/// <returns>Hashed string.</returns>
		public static ulong HashFileName( string s )
		{
			uint eax, ecx, edx, ebx, esi, edi;

			eax = ecx = edx = ebx = esi = edi = 0;
			ebx = edi = esi = (uint) s.Length + 0xDEADBEEF;

			int i = 0;

			for ( i = 0; i + 12 < s.Length; i += 12 )
			{
				edi = (uint) ( ( s[ i + 7 ] << 24 ) | ( s[ i + 6 ] << 16 ) | ( s[ i + 5 ] << 8 ) | s[ i + 4 ] ) + edi;
				esi = (uint) ( ( s[ i + 11 ] << 24 ) | ( s[ i + 10 ] << 16 ) | ( s[ i + 9 ] << 8 ) | s[ i + 8 ] ) + esi;
				edx = (uint) ( ( s[ i + 3 ] << 24 ) | ( s[ i + 2 ] << 16 ) | ( s[ i + 1 ] << 8 ) | s[ i ] ) - esi;

				edx = ( edx + ebx ) ^ ( esi >> 28 ) ^ ( esi << 4 );
				esi += edi;
				edi = ( edi - edx ) ^ ( edx >> 26 ) ^ ( edx << 6 );
				edx += esi;
				esi = ( esi - edi ) ^ ( edi >> 24 ) ^ ( edi << 8 );
				edi += edx;
				ebx = ( edx - esi ) ^ ( esi >> 16 ) ^ ( esi << 16 );
				esi += edi;
				edi = ( edi - ebx ) ^ ( ebx >> 13 ) ^ ( ebx << 19 );
				ebx += esi;
				esi = ( esi - edi ) ^ ( edi >> 28 ) ^ ( edi << 4 );
				edi += ebx;
			}

			if ( s.Length - i > 0 )
			{
				switch ( s.Length - i )
				{
					case 12:
						esi += (uint) s[ i + 11 ] << 24;
						goto case 11;
					case 11:
						esi += (uint) s[ i + 10 ] << 16;
						goto case 10;
					case 10:
						esi += (uint) s[ i + 9 ] << 8;
						goto case 9;
					case 9:
						esi += (uint) s[ i + 8 ];
						goto case 8;
					case 8:
						edi += (uint) s[ i + 7 ] << 24;
						goto case 7;
					case 7:
						edi += (uint) s[ i + 6 ] << 16;
						goto case 6;
					case 6:
						edi += (uint) s[ i + 5 ] << 8;
						goto case 5;
					case 5:
						edi += (uint) s[ i + 4 ];
						goto case 4;
					case 4:
						ebx += (uint) s[ i + 3 ] << 24;
						goto case 3;
					case 3:
						ebx += (uint) s[ i + 2 ] << 16;
						goto case 2;
					case 2:
						ebx += (uint) s[ i + 1 ] << 8;
						goto case 1;
					case 1:		
						ebx += (uint) s[ i ];
						break;
				}

				esi = ( esi ^ edi ) - ( ( edi >> 18 ) ^ ( edi << 14 ) );
				ecx = ( esi ^ ebx ) - ( ( esi >> 21 ) ^ ( esi << 11 ) );
				edi = ( edi ^ ecx ) - ( ( ecx >> 7 ) ^ ( ecx << 25 ) );
				esi = ( esi ^ edi ) - ( ( edi >> 16 ) ^ ( edi << 16 ) );
				edx = ( esi ^ ecx ) - ( ( esi >> 28 ) ^ ( esi << 4 ) );
				edi = ( edi ^ edx ) - ( ( edx >> 18 ) ^ ( edx << 14 ) );
				eax = ( esi ^ edi ) - ( ( edi >> 8 ) ^ ( edi << 24 ) );

				return ( (ulong) edi << 32 ) | eax;
			}

			return ( (ulong) esi << 32 ) | eax;
		}
		
		/// <summary>
		/// Computes KR hash of the <paramref name="s"/>.
		/// </summary>
		/// <param name="s">Char array to hash.</param>
		/// <returns>Hashed string.</returns>
		public static ulong HashFileName( char[] s )
		{
			uint eax, ecx, edx, ebx, esi, edi;

			eax = ecx = edx = ebx = esi = edi = 0;
			ebx = edi = esi = (uint) s.Length + 0xDEADBEEF;

			int i = 0;

			for ( i = 0; i + 12 < s.Length; i += 12 )
			{
				edi = (uint) ( ( s[ i + 7 ] << 24 ) | ( s[ i + 6 ] << 16 ) | ( s[ i + 5 ] << 8 ) | s[ i + 4 ] ) + edi;
				esi = (uint) ( ( s[ i + 11 ] << 24 ) | ( s[ i + 10 ] << 16 ) | ( s[ i + 9 ] << 8 ) | s[ i + 8 ] ) + esi;
				edx = (uint) ( ( s[ i + 3 ] << 24 ) | ( s[ i + 2 ] << 16 ) | ( s[ i + 1 ] << 8 ) | s[ i ] ) - esi;

				edx = ( edx + ebx ) ^ ( esi >> 28 ) ^ ( esi << 4 );
				esi += edi;
				edi = ( edi - edx ) ^ ( edx >> 26 ) ^ ( edx << 6 );
				edx += esi;
				esi = ( esi - edi ) ^ ( edi >> 24 ) ^ ( edi << 8 );
				edi += edx;
				ebx = ( edx - esi ) ^ ( esi >> 16 ) ^ ( esi << 16 );
				esi += edi;
				edi = ( edi - ebx ) ^ ( ebx >> 13 ) ^ ( ebx << 19 );
				ebx += esi;
				esi = ( esi - edi ) ^ ( edi >> 28 ) ^ ( edi << 4 );
				edi += ebx;
			}

			if ( s.Length - i > 0 )
			{
				switch ( s.Length - i )
				{
					case 12:
						esi += (uint) s[ i + 11 ] << 24;
						goto case 11;
					case 11:
						esi += (uint) s[ i + 10 ] << 16;
						goto case 10;
					case 10:
						esi += (uint) s[ i + 9 ] << 8;
						goto case 9;
					case 9:
						esi += (uint) s[ i + 8 ];
						goto case 8;
					case 8:
						edi += (uint) s[ i + 7 ] << 24;
						goto case 7;
					case 7:
						edi += (uint) s[ i + 6 ] << 16;
						goto case 6;
					case 6:
						edi += (uint) s[ i + 5 ] << 8;
						goto case 5;
					case 5:
						edi += (uint) s[ i + 4 ];
						goto case 4;
					case 4:
						ebx += (uint) s[ i + 3 ] << 24;
						goto case 3;
					case 3:
						ebx += (uint) s[ i + 2 ] << 16;
						goto case 2;
					case 2:
						ebx += (uint) s[ i + 1 ] << 8;
						goto case 1;
					case 1:
						ebx += (uint) s[ i ];
						break;
				}

				esi = ( esi ^ edi ) - ( ( edi >> 18 ) ^ ( edi << 14 ) );
				ecx = ( esi ^ ebx ) - ( ( esi >> 21 ) ^ ( esi << 11 ) );
				edi = ( edi ^ ecx ) - ( ( ecx >> 7 ) ^ ( ecx << 25 ) );
				esi = ( esi ^ edi ) - ( ( edi >> 16 ) ^ ( edi << 16 ) );
				edx = ( esi ^ ecx ) - ( ( esi >> 28 ) ^ ( esi << 4 ) );
				edi = ( edi ^ edx ) - ( ( edx >> 18 ) ^ ( edx << 14 ) );
				eax = ( esi ^ edi ) - ( ( edi >> 8 ) ^ ( edi << 24 ) );

				return ( (ulong) edi << 32 ) | eax;
			}

			return ( (ulong) esi << 32 ) | eax;
		}
		#endregion

		#region Dictionary
		private static Dictionary<ulong,string> m_Dictionary = new Dictionary<ulong,string>();
		
		/// <summary>
		/// Loads dictionary from <paramref name="fileName"/>.
		/// </summary>
		/// <param name="fileName">Path to dictionary file.</param>
		public static void LoadDictionary( string fileName )
		{
			if ( !File.Exists( fileName ) )
				throw new Exception( String.Format( "Cannot find {0}!", Path.GetFileName( fileName ) ) );

			using ( FileStream stream = new FileStream( fileName, FileMode.Open ) )
			{
				using ( BinaryReader reader = new BinaryReader( stream ) )
				{
					byte[] id = reader.ReadBytes( 4 );

					if ( id[ 0 ] != 'D' || id[ 1 ] != 'I' || id[ 2 ] != 'C' || id[ 3 ] != 0 )
						throw new Exception( String.Format( "{0} is not a Dictionary file!", Path.GetFileName( fileName ) ) );

					m_Dictionary.Clear();

					int version = reader.ReadByte();

					while ( stream.Position < stream.Length )
					{
						ulong hash = reader.ReadUInt64();
						string name = null;

						if ( reader.ReadByte() == 1 )
							name = reader.ReadString();

						if ( !m_Dictionary.ContainsKey( hash ) )
							m_Dictionary.Add( hash, name );
					}
				}
			}

			m_FileName = fileName;
			m_NewHashes = 0;
			m_NewFileNames = 0;
			m_Modified = false;
		}

		/// <summary>
		/// Saves dictionary to the <paramref name="path"/>.
		/// </summary>
		/// <param name="fileName">Path on the HD.</param>
		public static void SaveDictionary( string fileName )
		{
			using ( FileStream stream = new FileStream( fileName, FileMode.Create, FileAccess.Write ) )
			{
				using ( BinaryWriter writer = new BinaryWriter( stream ) )
				{
					writer.Write( 'D' );
					writer.Write( 'I' );
					writer.Write( 'C' );
					writer.Write( (byte) 0 );

					writer.Write( (byte) 1 ); // version
					
					foreach ( KeyValuePair<ulong,string> kvp in m_Dictionary )
					{
						writer.Write( (ulong) kvp.Key );

						if ( kvp.Value != null )
						{
							writer.Write( (byte) 1 );
							writer.Write( (string) kvp.Value );
						}
						else
							writer.Write( (byte) 0 );
					}
				}
			}
			
			m_NewHashes = 0;
			m_NewFileNames = 0;
			m_Modified = false;
		}

		/// <summary>
		/// Merges loaded dictionary with another dictionary.
		/// </summary>
		/// <param name="fileName">Location of the second dictionary.</param>
		public static void MergeDictionary( string fileName )
		{
			if ( !File.Exists( fileName ) )
				throw new Exception( String.Format( "Cannot find {0}!", Path.GetFileName( fileName ) ) );

			using ( FileStream stream = new FileStream( fileName, FileMode.Open ) )
			{
				using ( BinaryReader reader = new BinaryReader( stream ) )
				{
					byte[] id = reader.ReadBytes( 4 );

					if ( id[ 0 ] != 'D' || id[ 1 ] != 'I' || id[ 2 ] != 'C' || id[ 3 ] != 0 )
						throw new Exception( String.Format( "{0} is not a Dictionary file!", Path.GetFileName( fileName ) ) );

					int version = reader.ReadByte();

					while ( stream.Position < stream.Length )
					{
						ulong hash = reader.ReadUInt64();
						string name = null;

						if ( reader.ReadByte() == 1 )
							name = reader.ReadString();

						if ( m_Dictionary.ContainsKey( hash ) )
						{
							if ( m_Dictionary[ hash ] == null )
							{
								m_Dictionary[ hash ] = name;
								m_NewFileNames += 1;
								m_Modified = true;
							}
						}
						else
						{
							m_Dictionary.Add( hash, name );	

							m_NewHashes += 1;

							if ( name != null )
								m_NewFileNames += 1;

							m_Modified = true;
						}
					}
				}
			}
		}

		/// <summary>
		/// Checks if <paramref name="hash"/> is in the dictionary.
		/// </summary>
		/// <param name="hash">File name hash.</param>
		/// <returns>True if found, false otherwise.</returns>
		public static bool Contains( ulong hash )
		{
			if ( m_Dictionary.ContainsKey( hash ) )
				return true;

			return false;
		}

		/// <summary>
		/// Tries to retrieve file name binded to <paramref name="hash"/>.
		/// </summary>
		/// <param name="hash">File name hash.</param>
		/// <param name="add">Adds if hash doesn't exist.</param>
		/// <returns>File name.</returns>
		public static string Get( ulong hash, bool add )
		{
			string name;

			if ( m_Dictionary.ContainsKey( hash ) )
			{
				if ( m_Dictionary.TryGetValue( hash, out name ) )
					return name;
			}

			if ( add )
			{
				m_NewHashes += 1;
				m_Modified = true;
				m_Dictionary.Add( hash, null );
			}

			return null;
		}

		/// <summary>
		/// Tries to add <paramref name="name"/> binded to <paramref name="hash"/> to the dictionary. Doulbe
		/// </summary>
		/// <param name="hash">File name hash.</param>
		/// <param name="name">File name.</param>
		/// <returns>True if successful, false otherwise.</returns>
		public static bool Set( ulong hash, string name )
		{
			if ( m_Dictionary.ContainsKey( hash ) )
			{
				string value = m_Dictionary[ hash ];
				
				if ( value == null )
				{
					m_Dictionary[ hash ] = name;
					m_NewFileNames += 1;
					m_Modified = true;
					return true;
				}
			}
			else
			{
				m_NewHashes += 1;
				m_NewFileNames += 1;
				m_Modified = true;
				m_Dictionary.Add( hash, name );
			}
			
			return false;
		}

		/// <summary>
		/// Removes the file name with the specified hash from the dictionary.
		/// </summary>
		/// <param name="hash">The hash of the file name to remove.</param>
		/// <returns>true if the file name is successfully found and removed; otherwise, false.</returns>
		public static bool Unset( ulong hash )
		{
			bool ret = m_Dictionary.ContainsKey( hash );

			if ( m_Dictionary.ContainsKey( hash ) && m_Dictionary[ hash ] != null )
			{
				m_Dictionary[ hash ] = null;
				m_NewFileNames -= 1;
				m_Modified = true;
				return true;
			}

			return false;
		}
		#endregion
	}
}
